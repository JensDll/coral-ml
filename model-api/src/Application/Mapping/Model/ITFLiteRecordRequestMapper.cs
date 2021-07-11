using Application.Data.Models;
using Contracts.Request;
using Contracts.Response;
using Domain.DataTransfer;
using Domain.Entities;
using Domain.ValueObjects;
using Microsoft.AspNetCore.Http;
using System.Collections.Generic;

namespace Application.Mapping.Model
{
    public interface ITFLiteRecordRequestMapper
    {
        Pagination MapPaginationRequest(PaginationRequestDto paginationRequestDto);

        FormFileZipper MapCreateRequest(IFormFile model, IFormFile label);
    }
}
